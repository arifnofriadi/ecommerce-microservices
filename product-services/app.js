const express = require('express')
const app = express()

products = [
    {
        "id": 1,
        "name": "Product 1",
        "description": "Product 1 description",
        "price": 100
    },
    {
        "id": 2,
        "name": "Product 2",
        "description": "Product 2 description",
        "price": 200
    },
    {
        "id": 3,
        "name": "Product 3",
        "description": "Product 3 description",
        "price": 300
    }
];

app.get('/products', (req, res) => {
    res.send(products);
});

app.get('/products/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const product = products.find(p => p.id === id);

    if (!product) {
        return res.status(404).send('Product not found');
    }
    
    res.send(product);
});

app.listen(3000, () => {
    console.log('Listening on port 3000');
});