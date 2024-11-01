const express = require('express')
const app = express()
const sequelize = require('./database');
const { DataTypes } = require('sequelize');

// middleware for parsing JSON
app.use(express.json());

// define model product
const Product = sequelize.define('Product', {
    name: {
        type: DataTypes.STRING,
        allowNull: false
    },
    description: {
        type: DataTypes.STRING,
        allowNull: true
    },
    price: {
        type: DataTypes.FLOAT,
        allowNull: false
    }
});

const initDb = async () => {
    try {
        await sequelize.sync({ force: false }); // Use force: true if you want to drop and recreate the table
        console.log("Database & tables created!");
    } catch (error) {
        console.error("Error creating database tables:", error);
    }
};

initDb();

// sync model with database
sequelize.sync().then(() => {
    console.log('Products table synced with database');
});


const successResponse = (res, message, data = null) => {
    res.status(200).json({
        success: true,
        message: message,
        data: data
    });
}; 

const errorResponse = (res, status, message) => {
    res.status(status).json({
        success: false,
        message: message
    });
};

// get all product
app.get('/products', async (req, res) => {
    try {
        const products = await Product.findAll();
        successResponse(res, 'Products Retrieved Successfully', products);
    } catch (error) {
        console.log(error);
        errorResponse(res, 500, 'Error Retrieving Products');
    }
});

// get single product by id
app.get('/products/:id', async (req, res, next) => {
    try {
        const id = parseInt(req.params.id);
        const product = await Product.findByPk(id);
    
        if (!product) {
            // if product not found, throw error with status 404
            const error = new Error('Product Not Found');
            error.status = 404;
            throw error;
        }
        
        successResponse(res, 'Product Retrieved Successfully', product);     
    } catch (error) {
        next(error); // send error to middleware error handling
    }
});

// create new product
app.post('/products', async (req, res) => {
    try {
        const { name, description, price } = req.body;

        // input validation
        if (!name || !price) {
            return errorResponse(res, 400, 'Name and Price are required');
        }

        // create new product to database
        const newProduct = await Product.create({ name, description, price });
        successResponse(res, 'New Product Create', newProduct)
    } catch (error) {
        console.log(error)
        errorResponse(res, 500, 'Error Creating Product');
    }
});

// middleware to handling error
app.use((err, req, res, next) => {
    const statusCode = err.status || 500;
    res.status(statusCode).json({
        success: false,
        message: err.message || 'Internal Server Error'
    });
});

app.listen(3000, () => {
    console.log('Listening on port 3000');
});