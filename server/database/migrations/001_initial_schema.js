'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    // Tabela de jogadores
    await queryInterface.createTable('Players', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      username: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true
      },
      email: {
        type: Sequelize.STRING,
        allowNull: true,
        unique: true
      },
      password_hash: {
        type: Sequelize.STRING,
        allowNull: false
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
    });

    // Tabela de sessões de jogo
    await queryInterface.createTable('GameSessions', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      session_code: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true
      },
      host_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'Players',
          key: 'id'
        }
      },
      max_players: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 4
      },
      is_active: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        defaultValue: true
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
    });

    // Tabela de relacionamento entre jogadores e sessões
    await queryInterface.createTable('PlayerSessions', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      player_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'Players',
          key: 'id'
        }
      },
      session_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'GameSessions',
          key: 'id'
        }
      },
      is_ready: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        defaultValue: false
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
    });
  },

  down: async (queryInterface, Sequelize) => {
    // Ordem reversa para evitar problemas de chave estrangeira
    await queryInterface.dropTable('PlayerSessions');
    await queryInterface.dropTable('GameSessions');
    await queryInterface.dropTable('Players');
  }
};