<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Cart extends Model
{
    protected $table = 'cart_items';

    protected $fillable = [
        'product_id', 'name', 'quantity', 'price'
    ];
}
