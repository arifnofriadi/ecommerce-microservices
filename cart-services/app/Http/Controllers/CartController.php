<?php

namespace App\Http\Controllers;

class CartController extends Controller
{
    private $cartItems = [
        [
            'id' => 1,
            'name' => 'Product 1',
            'quantity' => 1,
            'price' => 100
        ],
        [
            'id' => 2,
            'name' => 'Product 2',
            'quantity' => 2,
            'price' => 200
        ],
        [
            'id' => 3,
            'name' => 'Product 3',
            'quantity' => 3,
            'price' => 300
        ]
    ];

    public function index()
    {
        return response()->json($this->cartItems);
    }

    public function show($id)
    {
        $total_quantity = array_reduce($this->cartItems, function ($total, $item) use ($id) {
            if ($item['id'] == $id) {
                $total += $item['quantity'];
            }
            return $total;
        }, 0);

        return response()->json([
            'product' => $id,
            'total_quantity' => $total_quantity
        ]);
    }
}
