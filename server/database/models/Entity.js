module.exports = (sequelize, DataTypes) => {
  const Entity = sequelize.define('Entity', {
    session_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'GameSessions',
        key: 'id'
      }
    },
    entity_type: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        isIn: [['player', 'enemy', 'npc', 'item']]
      }
    },
    x: {
      type: DataTypes.FLOAT,
      allowNull: false,
      defaultValue: 0,
      validate: {
        min: 0
      }
    },
    y: {
      type: DataTypes.FLOAT,
      allowNull: false,
      defaultValue: 0,
      validate: {
        min: 0
      }
    },
    health: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 100,
      validate: {
        min: 0
      }
    },
    max_health: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 100,
      validate: {
        min: 1
      }
    },
    data: {
      type: DataTypes.JSON,
      allowNull: true
    }
  }, {
    tableName: 'Entities',
    hooks: {
      beforeValidate: (entity) => {
        // Garante que os valores não sejam negativos
        if (entity.health < 0) entity.health = 0;
        if (entity.x < 0) entity.x = 0;
        if (entity.y < 0) entity.y = 0;
      }
    }
  });

  // Associações
  Entity.associate = function(models) {
    Entity.belongsTo(models.GameSession, {
      as: 'session',
      foreignKey: 'session_id'
    });
  };

  // Métodos de instância
  Entity.prototype.move = function(newX, newY) {
    this.x = newX;
    this.y = newY;
    return this.save();
  };
  
  Entity.prototype.takeDamage = function(amount) {
    this.health = Math.max(0, this.health - amount);
    return this.save();
  };
  
  Entity.prototype.heal = function(amount) {
    this.health = Math.min(this.max_health, this.health + amount);
    return this.save();
  };
  
  Entity.prototype.isAlive = function() {
    return this.health > 0;
  };
  
  Entity.prototype.getDistanceTo = function(otherEntity) {
    const dx = this.x - otherEntity.x;
    const dy = this.y - otherEntity.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  return Entity;
};