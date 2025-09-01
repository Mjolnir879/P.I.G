module.exports = (sequelize, DataTypes) => {
  const Item = sequelize.define('Item', {
    name: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        len: [1, 50]
      }
    },
    description: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    item_type: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        isIn: [['weapon', 'armor', 'consumable', 'material', 'quest']]
      }
    },
    value: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
      validate: {
        min: 0
      }
    },
    stats: {
      type: DataTypes.JSON,
      allowNull: true
    },
    createdAt: {
      type: DataTypes.TEXT, // Altera de INTEGER para TEXT
      allowNull: true,
      defaultValue: DataTypes.NOW, // Ou usar defaultValue: sequelize.literal('CURRENT_TIMESTAMP')
    },

    updatedAt: {
      type: DataTypes.TEXT, // Altera de INTEGER para TEXT,
      allowNull: true,
      defaultValue: DataTypes.NOW, // Ou usar defaultValue: sequelize.literal('CURRENT_TIMESTAMP')
    }

  }, {
    tableName: 'Items'
  });

  // Associações
  Item.associate = function(models) {
    Item.belongsToMany(models.Player, {
      through: 'PlayerItems',
      as: 'owners',
      foreignKey: 'item_id'
    });
  };

  // Métodos de instância
  Item.prototype.getStat = function(statName) {
    return this.stats ? this.stats[statName] || 0 : 0;
  };
  
  Item.prototype.isEquippable = function() {
    return ['weapon', 'armor'].includes(this.item_type);
  };
  
  Item.prototype.isConsumable = function() {
    return this.item_type === 'consumable';
  };

  return Item;
};