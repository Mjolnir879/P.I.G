const db = require('./database/models');

// Exemplo de uso
async function getPlayerStats(playerId) {
  return await db.Player.findByPk(playerId);
}

async function createGameSession(sessionData) {
  return await db.GameSession.create(sessionData);
}

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const { Sequelize, DataTypes } = require('sequelize');
const PORT = process.env.PORT || 3000;
// HOST configurável: '127.0.0.1' para localhost-only, '0.0.0.0' para aceitar conexões da LAN
const HOST = process.env.HOST || '0.0.0.0';


// Configuração do servidor :cite[7]
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Configuração do banco de dados :cite[5]
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, 'database/game.db')
});

// Definição de modelos do banco de dados
const Player = sequelize.define('Player', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  score: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  }
});

const GameSession = sequelize.define('GameSession', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  sessionCode: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  }
});

// Sincroniza o banco de dados
sequelize.sync();

// Estado do jogo
let gameState = {
  players: {},
  entities: [],
  lastUpdate: Date.now()
};

// Geração de ID único
function generateId() {
  return Math.random().toString(36).substr(2, 9);
}

// Sistema de IA para entidades não controláveis
class AIController {
  constructor(entity) {
    this.entity = entity;
    this.state = 'idle';
    this.stateTimer = 0;
    this.targetX = 0;
    this.targetY = 0;
  }

  update(deltaTime) {
    this.stateTimer -= deltaTime;
    
    if (this.stateTimer <= 0) {
      this.changeState();
    }
    
    this.executeState(deltaTime);
  }

  changeState() {
    const states = ['idle', 'wander', 'chase'];
    this.state = states[Math.floor(Math.random() * states.length)];
    this.stateTimer = Math.random() * 3000 + 1000; // 1-4 segundos
    
    if (this.state === 'wander') {
      // Define um alvo aleatório para vagar
      this.targetX = Math.random() * 800;
      this.targetY = Math.random() * 600;
    }
  }

  executeState(deltaTime) {
    const speed = 2;
    
    switch (this.state) {
      case 'idle':
        // Não faz nada
        break;
        
      case 'wander':
        // Move-se em direção ao alvo
        const dx = this.targetX - this.entity.x;
        const dy = this.targetY - this.entity.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 10) {
          this.entity.x += (dx / distance) * speed;
          this.entity.y += (dy / distance) * speed;
        }
        break;
        
      case 'chase':
        // Persegue o jogador mais próximo
        let closestPlayer = null;
        let closestDistance = Infinity;
        
        for (const playerId in gameState.players) {
          const player = gameState.players[playerId];
          const dx = player.x - this.entity.x;
          const dy = player.y - this.entity.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < closestDistance) {
            closestDistance = distance;
            closestPlayer = player;
          }
        }
        
        if (closestPlayer && closestDistance < 300) {
          const dx = closestPlayer.x - this.entity.x;
          const dy = closestPlayer.y - this.entity.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          this.entity.x += (dx / distance) * speed;
          this.entity.y += (dy / distance) * speed;
        }
        break;
    }
  }
}

// Manipuladores de Socket.IO
io.on('connection', (socket) => {
  console.log('Novo cliente conectado:', socket.id);
  
  // Adiciona jogador ao estado do jogo
  gameState.players[socket.id] = {
    id: socket.id,
    x: Math.random() * 400 + 200,
    y: Math.random() * 400 + 100,
    health: 100,
    score: 0
  };
  
  // Envia estado inicial para o novo cliente
  socket.emit('game_state', gameState);
  
  // Notifica outros jogadores
  socket.broadcast.emit('player_joined', gameState.players[socket.id]);
  
  // Manipula entrada do jogador
  socket.on('player_input', (inputData) => {
    if (gameState.players[socket.id]) {
      const player = gameState.players[socket.id];
      const speed = 5;
      
      // Atualiza posição baseada na entrada
      if (inputData.up) player.y -= speed;
      if (inputData.down) player.y += speed;
      if (inputData.left) player.x -= speed;
      if (inputData.right) player.x += speed;
      
      // Mantém o jogador dentro dos limites
      player.x = Math.max(0, Math.min(800 - 50, player.x));
      player.y = Math.max(0, Math.min(600 - 50, player.y));
    }
  });
  
  // Manipula ações do jogador (ataques)
  socket.on('player_action', (actionData) => {
    if (actionData.type === 'attack') {
      // Verifica se acertou alguma entidade
      gameState.entities.forEach(entity => {
        const dx = entity.x - actionData.target_x;
        const dy = entity.y - actionData.target_y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 50) { // Raio de ataque
          entity.health -= 10;
          if (entity.health <= 0) {
            // Entidade derrotada
            gameState.players[socket.id].score += 10;
          }
        }
      });
    }
  });
  
  // Manipula desconexão
  socket.on('disconnect', () => {
    console.log('Cliente desconectado:', socket.id);
    delete gameState.players[socket.id];
    socket.broadcast.emit('player_left', socket.id);
  });
});

// Loop de atualização do jogo
setInterval(() => {
  const now = Date.now();
  const deltaTime = now - gameState.lastUpdate;
  gameState.lastUpdate = now;
  
  // Atualiza entidades com IA
  gameState.entities.forEach(entity => {
    if (entity.aiController) {
      entity.aiController.update(deltaTime);
    }
  });
  
  // Envia atualização de estado para todos os clientes
  io.emit('game_state_update', gameState);
}, 1000 / 60); // 60 updates por segundo

// Inicia o servidor :cite[7]
server.listen(PORT, HOST, () => {
  console.log(`Servidor executando em http://${HOST === '0.0.0.0' ? '0.0.0.0 (todas interfaces)' : HOST}:${PORT}`);
  // imprime endereços locais para conveniência (não obrigatório)
  try {
    const os = require('os');
    const ifaces = os.networkInterfaces();
    Object.keys(ifaces).forEach(name => {
      ifaces[name].forEach(iface => {
        if (iface.family === 'IPv4' && !iface.internal) {
          console.log(` - LAN IP: http://${iface.address}:${PORT}`);
        }
      });
    });
  } catch (err) {}
});