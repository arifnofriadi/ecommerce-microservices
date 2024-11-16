const express = require('express')
const app = express()
const sequelize = require('./database');
const { DataTypes } = require('sequelize');
const cors = require('cors');

// middleware for parsing JSON
app.use(express.json());
app.use(cors());

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

// initialize database
const initDb = async () => {
    try {
        await sequelize.sync({ alter: true }); // Use force: true if you want to drop and recreate the table
        console.log("Products table synced with database");
    } catch (error) {
        console.error("Error creating database tables:", error);
    }
};

initDb();


// standar response function
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

// update product
app.put('/products/:id', async (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const { name, description, price } = req.body;

        // input validation
        if (!name || !price) {
            return errorResponse(res, 400, 'Name and Price are required');
        }

        // find product by id   
        const product = await Product.findByPk(id);
        if (!product) {
            return errorResponse(res, 404, 'Product Not Found');
        }

        product.name = name || product.name;
        product.description = description || product.description;
        product.price = price || product.price;

        // update product
        await product.save();
        successResponse(res, 'Product Updated', product);
    } catch (error) {
        console.log(error);
        errorResponse(res, 500, 'Error Updating Product');
    }
});

// delete product
app.delete('/products/:id', async (req, res) => {
    try {
        const id = parseInt(req.params.id);
        const product = await Product.findByPk(id);

        if (!product) {
            return errorResponse(res, 404, 'Product Not Found');
        }
        
        await product.destroy();
        successResponse(res, 'Product Deleted');
    } catch (error) {
        console.log(error);
        errorResponse(res, 500, 'Error Deleting Product');
    }
});

// error handling middleware
app.use((err, req, res, next) => {
    const statusCode = err.status || 500;
    console.error(err.stack);
    res.status(statusCode).json({
        success: false,
        message: err.message || 'Internal Server Error'
    });
});

app.listen(3000, () => {
    console.log('Listening on port 3000');
});