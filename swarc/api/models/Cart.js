const mongoose = require('mongoose');

const CartSchema = new mongoose.Schema(
    {
    userId:{type: 'string', required: true },
    products:[
        {
            productId:{type:'string' },
            quantity:{type: 'number', default: 1 }
        }
    ],
},
    {timestamps: true}
    );

    module.exports = mongoose.model('Cart', CartSchema);
