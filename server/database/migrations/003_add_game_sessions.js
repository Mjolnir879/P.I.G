'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    const { sequelize } = queryInterface;
    
    // Função para verificar se uma coluna existe
    const columnExists = async (tableName, columnName) => {
      try {
        const [results] = await sequelize.query(
          `PRAGMA table_info(${tableName})`
        );
        return results.some(col => col.name === columnName);
      } catch (error) {
        console.error(`Erro ao verificar coluna ${columnName}:`, error);
        return false;
      }
    };

    // Função para verificar se uma tabela existe
    const tableExists = async (tableName) => {
      try {
        const [results] = await sequelize.query(
          `SELECT name FROM sqlite_master WHERE type='table' AND name='${tableName}'`
        );
        return results.length > 0;
      } catch (error) {
        console.error(`Erro ao verificar tabela ${tableName}:`, error);
        return false;
      }
    };

    // Adiciona colunas apenas se não existirem
    if (!(await columnExists('GameSessions', 'map_name'))) {
      await queryInterface.addColumn('GameSessions', 'map_name', {
        type: Sequelize.STRING,
        allowNull: false,
        defaultValue: 'forest'
      });
    }

    if (!(await columnExists('GameSessions', 'game_mode'))) {
      await queryInterface.addColumn('GameSessions', 'game_mode', {
        type: Sequelize.STRING,
        allowNull: false,
        defaultValue: 'coop'
      });
    }

    if (!(await columnExists('GameSessions', 'difficulty'))) {
      await queryInterface.addColumn('GameSessions', 'difficulty', {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 1
      });
    }

    // Cria tabela de entidades do jogo se não existir
    if (!(await tableExists('Entities'))) {
      await queryInterface.createTable('Entities', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        session_id: {
          type: Sequelize.INTEGER,
          allowNull: false,
          references: {
            model: 'GameSessions',
            key: 'id'
          }
        },
        entity_type: {
          type: Sequelize.STRING,
          allowNull: false
        },
        x: {
          type: Sequelize.FLOAT,
          allowNull: false,
          defaultValue: 0
        },
        y: {
          type: Sequelize.FLOAT,
          allowNull: false,
          defaultValue: 0
        },
        health: {
          type: Sequelize.INTEGER,
          allowNull: false,
          defaultValue: 100
        },
        max_health: {
          type: Sequelize.INTEGER,
          allowNull: false,
          defaultValue: 100
        },
        data: {
          type: Sequelize.JSON,
          allowNull: true
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
    }

    // Cria tabela de itens se não existir
    if (!(await tableExists('Items'))) {
      await queryInterface.createTable('Items', {
        id: {
          type: Sequelize.INTEGER,
          primaryKey: true,
          autoIncrement: true
        },
        name: {
          type: Sequelize.STRING,
          allowNull: false
        },
        description: {
          type: Sequelize.TEXT,
          allowNull: true
        },
        item_type: {
          type: Sequelize.STRING,
          allowNull: false
        },
        value: {
          type: Sequelize.INTEGER,
          allowNull: false,
          defaultValue: 0
        },
        stats: {
          type: Sequelize.JSON,
          allowNull: true
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
    }

    // Cria tabela de relacionamento entre jogadores e itens se não existir
    if (!(await tableExists('PlayerItems'))) {
      await queryInterface.createTable('PlayerItems', {
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
        item_id: {
          type: Sequelize.INTEGER,
          allowNull: false,
          references: {
            model: 'Items',
            key: 'id'
          }
        },
        quantity: {
          type: Sequelize.INTEGER,
          allowNull: false,
          defaultValue: 1
        },
        equipped: {
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
    }
  },

  down: async (queryInterface, Sequelize) => {
    // Remove as colunas adicionadas e tabelas
    await queryInterface.removeColumn('GameSessions', 'map_name');
    await queryInterface.removeColumn('GameSessions', 'game_mode');
    await queryInterface.removeColumn('GameSessions', 'difficulty');
    
    await queryInterface.dropTable('PlayerItems');
    await queryInterface.dropTable('Items');
    await queryInterface.dropTable('Entities');
  }
};