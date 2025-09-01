const { sequelize } = require('../models');
const fs = require('fs');
const path = require('path');

async function migrateDatabase() {
  try {
    console.log('Executando migrações do banco de dados...');
    
    // Executa migrações pendentes
    const migrationsPath = path.join(__dirname, '..', 'migrations');
    const migrationFiles = fs.readdirSync(migrationsPath).sort();
    
    for (const file of migrationFiles) {
      if (file.endsWith('.js')) {
        const migration = require(path.join(migrationsPath, file));
        await migration.up(sequelize.getQueryInterface(), sequelize.Sequelize);
        console.log(`Migração ${file} executada com sucesso!`);
      }
    }
    
    console.log('Todas as migrações foram executadas com sucesso!');
  } catch (error) {
    console.error('Erro ao executar migrações:', error);
  } finally {
    await sequelize.close();
  }
}

// Executa as migrações se este script for chamado diretamente
if (require.main === module) {
  migrateDatabase();
}

module.exports = migrateDatabase;