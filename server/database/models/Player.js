module.exports = (sequelize, DataTypes) => {
  const Player = sequelize.define('Player', {
    username: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      validate: {
        len: [3, 20],
        isAlphanumeric: true
      }
    },
    email: {
      type: DataTypes.STRING,
      allowNull: true,
      unique: true,
      validate: {
        isEmail: true
      }
    },
    password_hash: {
      type: DataTypes.STRING,
      allowNull: false
    },
    level: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 1,
      validate: {
        min: 1,
        max: 100
      }
    },
    experience: {
      type: DataTypes.INTEGER,
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
    strength: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 10,
      validate: {
        min: 1,
        max: 100
      }
    },
    dexterity: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 8,
      validate: {
        min: 1,
        max: 100
      }
    },
    intelligence: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 5,
      validate: {
        min: 1,
        max: 100
      }
    },
    vitality: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 12,
      validate: {
        min: 1,
        max: 100
      }
    },
    gold: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
      validate: {
        min: 0
      }
    }
  }, {
    tableName: 'Players',
    hooks: {
      beforeValidate: (player) => {
        // Garante que os valores não sejam negativos
        if (player.health < 0) player.health = 0;
        if (player.experience < 0) player.experience = 0;
        if (player.gold < 0) player.gold = 0;
      }
    }
  });

  // Associações
  Player.associate = function(models) {
    Player.belongsToMany(models.GameSession, {
      through: 'PlayerSessions',
      as: 'sessions',
      foreignKey: 'player_id'
    });
    
    Player.belongsToMany(models.Item, {
      through: 'PlayerItems',
      as: 'items',
      foreignKey: 'player_id'
    });
    
    Player.hasMany(models.GameSession, {
      as: 'hostedSessions',
      foreignKey: 'host_id'
    });
  };

  // Métodos de instância
  Player.prototype.addExperience = function(amount) {
    this.experience += amount;
    
    // Verifica se subiu de nível
    const expForNextLevel = this.level * 100;
    if (this.experience >= expForNextLevel) {
      this.levelUp();
    }
    
    return this.save();
  };
  
  Player.prototype.levelUp = function() {
    this.level += 1;
    this.max_health += 10;
    this.health = this.max_health; // Cura completamente ao subir de nível
    this.strength += 2;
    this.dexterity += 1;
    this.intelligence += 1;
    this.vitality += 3;
    
    // Reseta a experiência para o próximo nível
    this.experience = 0;
    
    return this.save();
  };
  
  Player.prototype.takeDamage = function(amount) {
    this.health = Math.max(0, this.health - amount);
    return this.save();
  };
  
  Player.prototype.heal = function(amount) {
    this.health = Math.min(this.max_health, this.health + amount);
    return this.save();
  };
  
  Player.prototype.addGold = function(amount) {
    this.gold += amount;
    return this.save();
  };
  
  Player.prototype.isAlive = function() {
    return this.health > 0;
  };

  return Player;
};