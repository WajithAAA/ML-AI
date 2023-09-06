const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema(
    {
    title:{type: 'string', required: true, unique: true},
    desc:{type:'string', required: true},
    img:{type:'string', required: true},
    categoies:{type:'array'},
    size:{type:'array'},
    color:{type:'array' },
    price:{type: 'number', required: true},
    inStore:{type:'boolean', default: true},
    },
    {timestamps: true}
    );

    module.exports = mongoose.model('Product', ProductSchema);
