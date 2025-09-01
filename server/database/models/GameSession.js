module.exports = (sequelize, DataTypes) => {
  const GameSession = sequelize.define('GameSession', {
    session_code: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      validate: {
        len: [6, 10],
        isAlphanumeric: true
      }
    },
    host_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Players',
        key: 'id'
      }
    },
    max_players: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 4,
      validate: {
        min: 1,
        max: 16
      }
    },
    is_active: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: true
    },
    map_name: {
      type: DataTypes.STRING,
      allowNull: false,
      defaultValue: 'forest'
    },
    game_mode: {
      type: DataTypes.STRING,
      allowNull: false,
      defaultValue: 'coop',
      validate: {
        isIn: [['coop', 'pvp', 'survival']]
      }
    },
    difficulty: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 1,
      validate: {
        min: 1,
        max: 5
      }
    }
  }, {
    tableName: 'GameSessions'
  });

  // Associações
  GameSession.associate = function(models) {
    GameSession.belongsTo(models.Player, {
      as: 'host',
      foreignKey: 'host_id'
    });
    
    GameSession.belongsToMany(models.Player, {
      through: 'PlayerSessions',
      as: 'players',
      foreignKey: 'session_id'
    });
    
    GameSession.hasMany(models.Entity, {
      as: 'entities',
      foreignKey: 'session_id'
    });
  };

  // Métodos de instância
  GameSession.prototype.getPlayerCount = function() {
    return this.countPlayers();
  };
  
  GameSession.prototype.isFull = function() {
    return this.getPlayerCount().then(count => {
      return count >= this.max_players;
    });
  };
  
  GameSession.prototype.addPlayer = function(playerId) {
    return this.addPlayer(playerId);
  };
  
  GameSession.prototype.removePlayer = function(playerId) {
    return this.removePlayer(playerId);
  };
  
  GameSession.prototype.getAllPlayersReady = function() {
    return this.getPlayers({
      where: {
        is_ready: true
      }
    }).then(players => {
      return this.getPlayerCount().then(count => {
        return players.length === count;
      });
    });
  };

  return GameSession;
};