const { sequelize, Sequelize } = require('../models');
const fs = require('fs');
const path = require('path');

async function recreateDatabase() {
  try {
    console.log('Recriando banco de dados...');
    
    // Fecha a conexão atual se estiver aberta
    if (sequelize.connectionManager.hasOwnProperty('connections') && 
        Object.keys(sequelize.connectionManager.connections).length > 0) {
      await sequelize.close();
      console.log('Conexão anterior fechada.');
    }
    
    // Remove o arquivo do banco de dados existente
    const dbPath = path.join(__dirname, '..', 'game.db');
    if (fs.existsSync(dbPath)) {
      fs.unlinkSync(dbPath);
      console.log('Banco de dados antigo removido.');
    }
    
    // Recria a conexão usando a instância existente do sequelize
    await sequelize.authenticate();
    console.log('Novo banco de dados criado e conectado.');
    
    // Desativa o sincronismo automático para usar migrações manuais
    await sequelize.sync({ force: false });
    
    // Executa todas as migrações manualmente
    const migrationsPath = path.join(__dirname, '..', 'migrations');
    const migrationFiles = fs.readdirSync(migrationsPath)
      .filter(file => file.endsWith('.js'))
      .sort();
    
    for (const file of migrationFiles) {
      console.log(`Executando migração: ${file}`);
      const migration = require(path.join(migrationsPath, file));
      await migration.up(sequelize.getQueryInterface(), Sequelize);
      console.log(`Migração ${file} executada com sucesso!`);
    }
    
    // Executa os seeders
    const seedersPath = path.join(__dirname, '..', 'seeders');
    if (fs.existsSync(seedersPath)) {
      const seederFiles = fs.readdirSync(seedersPath)
        .filter(file => file.endsWith('.js'))
        .sort();
      
      for (const file of seederFiles) {
        console.log(`Executando seeder: ${file}`);
        const seeder = require(path.join(seedersPath, file));
        await seeder.up(sequelize.getQueryInterface(), Sequelize);
        console.log(`Seeder ${file} executado com sucesso!`);
      }
    } else {
      console.log('Pasta de seeders não encontrada, pulando...');
    }
    
    console.log('Banco de dados recriado com sucesso!');
  } catch (error) {
    console.error('Erro ao recriar banco de dados:', error);
  } finally {
    // Fecha a conexão ao finalizar
    if (sequelize.connectionManager.hasOwnProperty('connections') && 
        Object.keys(sequelize.connectionManager.connections).length > 0) {
      await sequelize.close();
      console.log('Conexão final fechada.');
    }
  }
}

// Executa se chamado diretamente
if (require.main === module) {
  recreateDatabase().then(() => {
    console.log('Processo de recriação concluído.');
    process.exit(0);
  }).catch(error => {
    console.error('Falha na recriação do banco:', error);
    process.exit(1);
  });
}

module.exports = recreateDatabase;