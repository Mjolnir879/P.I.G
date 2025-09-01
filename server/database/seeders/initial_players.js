'use strict';
const bcrypt = require('bcrypt');

module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Cria alguns jogadores de exemplo
    const passwordHash = await bcrypt.hash('password123', 10);
    
    return queryInterface.bulkInsert('Players', [
      {
        username: 'player1',
        email: 'player1@example.com',
        password_hash: passwordHash,
        level: 5,
        experience: 250,
        health: 100,
        max_health: 100,
        strength: 15,
        dexterity: 12,
        intelligence: 8,
        vitality: 14,
        gold: 500,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        username: 'player2',
        email: 'player2@example.com',
        password_hash: passwordHash,
        level: 3,
        experience: 150,
        health: 80,
        max_health: 80,
        strength: 10,
        dexterity: 15,
        intelligence: 10,
        vitality: 10,
        gold: 250,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        username: 'player3',
        email: 'player3@example.com',
        password_hash: passwordHash,
        level: 7,
        experience: 600,
        health: 120,
        max_health: 120,
        strength: 12,
        dexterity: 10,
        intelligence: 16,
        vitality: 12,
        gold: 1000,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ], {});
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Players', null, {});
  }
};