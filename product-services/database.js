const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('productdb', 'root', 'Dev@root23', {
    host: process.env.DB_HOST,
    dialect: 'mysql',
    port: 3306
});

module.exports = sequelize;