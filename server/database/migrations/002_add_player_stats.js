'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    const { sequelize } = queryInterface;
    
    // Função para verificar se uma coluna existe
    const columnExists = async (tableName, columnName) => {
      const [results] = await sequelize.query(
        `PRAGMA table_info(${tableName})`
      );
      return results.some(col => col.name === columnName);
    };
    
    // Adiciona colunas apenas se não existirem
    const columnsToAdd = [
      { name: 'level', type: Sequelize.INTEGER, defaultValue: 1 },
      { name: 'experience', type: Sequelize.INTEGER, defaultValue: 0 },
      { name: 'health', type: Sequelize.INTEGER, defaultValue: 100 },
      { name: 'max_health', type: Sequelize.INTEGER, defaultValue: 100 },
      { name: 'strength', type: Sequelize.INTEGER, defaultValue: 10 },
      { name: 'dexterity', type: Sequelize.INTEGER, defaultValue: 8 },
      { name: 'intelligence', type: Sequelize.INTEGER, defaultValue: 5 },
      { name: 'vitality', type: Sequelize.INTEGER, defaultValue: 12 },
      { name: 'gold', type: Sequelize.INTEGER, defaultValue: 0 }
    ];
    
    for (const column of columnsToAdd) {
      if (!(await columnExists('Players', column.name))) {
        await queryInterface.addColumn('Players', column.name, {
          type: column.type,
          allowNull: false,
          defaultValue: column.defaultValue
        });
        console.log(`Coluna ${column.name} adicionada.`);
      } else {
        console.log(`Coluna ${column.name} já existe, pulando.`);
      }
    }
  },

  down: async (queryInterface, Sequelize) => {
    // Remove as colunas adicionadas
    await queryInterface.removeColumn('Players', 'level');
    await queryInterface.removeColumn('Players', 'experience');
    await queryInterface.removeColumn('Players', 'health');
    await queryInterface.removeColumn('Players', 'max_health');
    await queryInterface.removeColumn('Players', 'strength');
    await queryInterface.removeColumn('Players', 'dexterity');
    await queryInterface.removeColumn('Players', 'intelligence');
    await queryInterface.removeColumn('Players', 'vitality');
    await queryInterface.removeColumn('Players', 'gold');
  }
};