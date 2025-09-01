'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Primeiro, vamos obter a sessão de jogo padrão
    const sessions = await queryInterface.sequelize.query(
      'SELECT id FROM GameSessions WHERE session_code = "DEFAULT"',
      { type: queryInterface.sequelize.QueryTypes.SELECT }
    );
    
    if (sessions.length === 0) {
      console.log('Nenhuma sessão DEFAULT encontrada. Pulando seed de entidades.');
      return;
    }
    
    const sessionId = sessions[0].id;
    
    // Cria algumas entidades de exemplo para a sessão
    return queryInterface.bulkInsert('Entities', [
      {
        session_id: sessionId,
        entity_type: 'npc',
        x: 300,
        y: 200,
        health: 100,
        max_health: 100,
        data: JSON.stringify({
          name: 'Mercador',
          dialogue: 'Bem-vindo à minha loja!',
          items: [1, 2, 3]
        }),
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        session_id: sessionId,
        entity_type: 'enemy',
        x: 500,
        y: 400,
        health: 50,
        max_health: 50,
        data: JSON.stringify({
          name: 'Goblin',
          damage: 10,
          exp: 25,
          loot: [3, 4]
        }),
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        session_id: sessionId,
        entity_type: 'item',
        x: 200,
        y: 300,
        health: 1,
        max_health: 1,
        data: JSON.stringify({
          item_id: 3,
          quantity: 1
        }),
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ], {});
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Entities', null, {});
  }
};