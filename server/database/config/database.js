const path = require('path');

module.exports = {
  development: {
    dialect: 'sqlite',
    storage: path.join(__dirname, '..', 'game.db'),
    logging: console.log,
    define: {
      timestamps: true,
      underscored: false,
      freezeTableName: true
    }
  },
  test: {
    dialect: 'sqlite',
    storage: ':memory:',
    logging: false,
    define: {
      timestamps: true,
      underscored: false,
      freezeTableName: true
    }
  },
  production: {
    dialect: 'sqlite',
    storage: path.join(__dirname, '..', 'game.db'),
    logging: false,
    define: {
      timestamps: true,
      underscored: false,
      freezeTableName: true
    }
  }
};