const { sequelize } = require('../models');
const fs = require('fs');
const path = require('path');

async function initDatabase() {
  try {
    console.log('Inicializando banco de dados...');
    
    // Sincroniza o banco de dados (cria tabelas se não existirem)
    await sequelize.sync({ force: true });
    console.log('Tabelas criadas com sucesso!');
    
    // Executa migrações
    const migrationsPath = path.join(__dirname, '..', 'migrations');
    const migrationFiles = fs.readdirSync(migrationsPath).sort();
    
    for (const file of migrationFiles) {
      if (file.endsWith('.js')) {
        const migration = require(path.join(migrationsPath, file));
        await migration.up(sequelize.getQueryInterface(), sequelize.Sequelize);
        console.log(`Migração ${file} executada com sucesso!`);
      }
    }
    
    // Executa seeders
    const seedersPath = path.join(__dirname, '..', 'seeders');
    const seederFiles = fs.readdirSync(seedersPath).sort();
    
    for (const file of seederFiles) {
      if (file.endsWith('.js')) {
        const seeder = require(path.join(seedersPath, file));
        await seeder.up(sequelize.getQueryInterface(), sequelize.Sequelize);
        console.log(`Seeder ${file} executado com sucesso!`);
      }
    }
    
    console.log('Banco de dados inicializado com sucesso!');
  } catch (error) {
    console.error('Erro ao inicializar banco de dados:', error);
  } finally {
    await sequelize.close();
  }
}

// Executa a inicialização se este script for chamado diretamente
if (require.main === module) {
  initDatabase();
}

module.exports = initDatabase;