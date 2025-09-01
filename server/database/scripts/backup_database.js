const { sequelize } = require('../models');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

async function backupDatabase() {
  try {
    console.log('Criando backup do banco de dados...');
    
    const backupDir = path.join(__dirname, '..', '..', 'backups');
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFile = path.join(backupDir, `backup-${timestamp}.sqlite`);
    
    // Copia o arquivo do banco de dados
    const dbFile = path.join(__dirname, '..', 'game.db');
    
    if (fs.existsSync(dbFile)) {
      fs.copyFileSync(dbFile, backupFile);
      console.log(`Backup criado: ${backupFile}`);
    } else {
      console.log('Arquivo de banco de dados não encontrado. Nada para fazer backup.');
    }
  } catch (error) {
    console.error('Erro ao criar backup:', error);
  }
}

// Executa o backup se este script for chamado diretamente
if (require.main === module) {
  backupDatabase();
}

module.exports = backupDatabase;