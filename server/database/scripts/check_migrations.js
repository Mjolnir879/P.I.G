// database/scripts/check_migrations.js
const { sequelize } = require('../models');
const fs = require('fs');
const path = require('path');

async function checkMigrations() {
  try {
    console.log('Verificando estado das migrações...');
    
    // Verifica se a tabela de controle de migrações existe
    const [results] = await sequelize.query(`
      SELECT name FROM sqlite_master 
      WHERE type='table' AND name='SequelizeMeta'
    `);
    
    if (results.length === 0) {
      console.log('Tabela de controle de migrações não existe.');
      return false;
    }
    
    // Obtém migrações executadas
    const [executedMigrations] = await sequelize.query(
      'SELECT name FROM SequelizeMeta'
    );
    
    console.log('Migrações executadas:');
    executedMigrations.forEach(migration => {
      console.log(`- ${migration.name}`);
    });
    
    return true;
  } catch (error) {
    console.error('Erro ao verificar migrações:', error);
    return false;
  }
}

if (require.main === module) {
  checkMigrations().then(success => {
    if (success) {
      console.log('Verificação concluída.');
    } else {
      console.log('Verificação falhou.');
    }
    process.exit(0);
  });
}

module.exports = checkMigrations;