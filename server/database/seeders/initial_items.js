'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Cria alguns itens de exemplo
    return queryInterface.bulkInsert('Items', [
      {
        name: 'Espada de Ferro',
        description: 'Uma espada resistente feita de ferro forjado',
        item_type: 'weapon',
        value: 100,
        stats: JSON.stringify({ damage: 15, speed: 1.0 }),
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        name: 'Armadura de Couro',
        description: 'Armadura leve feita de couro endurecido',
        item_type: 'armor',
        value: 75,
        stats: JSON.stringify({ defense: 10, agility: 5 }),
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        name: 'Poção de Cura',
        description: 'Restaura 50 pontos de vida',
        item_type: 'consumable',
        value: 25,
        stats: JSON.stringify({ heal: 50 }),
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        name: 'Arco Longo',
        description: 'Um arco longo para ataques à distância',
        item_type: 'weapon',
        value: 120,
        stats: JSON.stringify({ damage: 12, range: 10 }),
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        name: 'Elmo de Aço',
        description: 'Proteção robusta para a cabeça',
        item_type: 'armor',
        value: 60,
        stats: JSON.stringify({ defense: 8 }),
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ], {});
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Items', null, {});
  }
};