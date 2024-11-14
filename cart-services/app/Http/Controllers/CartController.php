<?php

namespace App\Http\Controllers;
use App\Models\Cart;
use Illuminate\Http\Request;
use App\Helpers\ResponseHelper;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;

class CartController extends Controller
{
    private $client;


    public function __construct()
    {
        $this->client = new \GuzzleHttp\Client(['base_uri' => 'http://localhost:3000']);
    }

    public function getProduct($productId = null)
    {
        try {
            $url = $productId ? "/products/{$productId}" : '/products';
            $response = $this->client->request('GET', $url);
            $responseData = json_decode($response->getBody()->getContents(), true);

            if ($response->getStatusCode() === 200 && isset($responseData['data'])) {
                return $responseData['data'];
            }

            return null;
        } catch (\Throwable $th) {
            Log::error([
                'message' => $th->getMessage(),
                'file' => $th->getFile(),
                'line' => $th->getLine()
            ]);

            return null;
        }

    }

    public function showProduct()
    {
        try {
            $cartItems = $this->getProduct();
            return ResponseHelper::successResponse('Cart items fetched successfully', $cartItems);
        } catch (\Throwable $th) {
            Log::error([
                'message' => $th->getMessage(),
                'file' => $th->getFile(),
                'line' => $th->getLine()
            ]);

            return ResponseHelper::errorResponse($th->getMessage());
        }
    }

    public function index()
    {
        try {
            $cartItems = Cart::orderBy('created_at', 'desc')->get();
            return ResponseHelper::successResponse('Cart items fetched successfully', $cartItems);
        } catch (\Throwable $th) {
            Log::error([
                'message' => $th->getMessage(),
                'file' => $th->getFile(),
                'line' => $th->getLine()
            ]);

            return ResponseHelper::errorResponse($th->getMessage());
        }
    }

    public function show($id)
    {
        try {
            $cartItem = Cart::find($id);
            if (!$cartItem)return ResponseHelper::errorResponse('Cart item not found', 404);

            return ResponseHelper::successResponse('Cart item fetched successfully', $cartItem);
        } catch (\Throwable $th) {
            Log::error([
                'message' => $th->getMessage(),
                'file' => $th->getFile(),
                'line' => $th->getLine()
            ]);

            return ResponseHelper::errorResponse($th->getMessage());
        }
    }

    public function store(Request $request)
    {
        $validate = $this->validate($request, [
            'product_id'    => 'required|integer',
            'quantity'      => 'required|integer'
        ]);

        try {
            $product = $this->getProduct($validate['product_id']);

            if (!$product) return ResponseHelper::errorResponse('Product not found', 404);

            $cartItem = Cart::create([
                'product_id'    => $validate['product_id'],
                'name'          => $product['name'],
                'quantity'      => $validate['quantity'],
                'price'         => $product['price'] *$validate['quantity']
            ]);

            if (!$cartItem) return ResponseHelper::errorResponse('Failed to create cart item', 500);

            return ResponseHelper::successResponse('Cart item created successfully', $cartItem);
        } catch (\Throwable $th) {
            Log::error([
                'message' => $th->getMessage(),
                'file' => $th->getFile(),
                'line' => $th->getLine()
            ]);

            return ResponseHelper::errorResponse($th->getMessage());
        }
    }

    public function update(Request $request, $id)
    {
        $validate = $this->validate($request, [
            'quantity'      => 'required|integer'
        ]);

        try {
            $cartItem = Cart::find($id);
            if (!$cartItem)return ResponseHelper::errorResponse('Cart item not found', 404);

            // get original price from product
            $product = $this->getProduct($cartItem->product_id);

            if (!$product || !isset($product['price'])) {
                return ResponseHelper::errorResponse('Product not found or price unavailable', 404);
            }

            $originalPrice = $product['price'];

            $cartItem->quantity = $validate['quantity'];
            $cartItem->price = $originalPrice * $validate['quantity'];
            $cartItem->save();

            return ResponseHelper::successResponse('Cart item updated successfully', $cartItem);
        } catch (\Throwable $th) {
            Log::error([
                'message' => $th->getMessage(),
                'file' => $th->getFile(),
                'line' => $th->getLine()
            ]);

            return ResponseHelper::errorResponse($th->getMessage());
        }
    }

   public function destroy($id)
   {
       try {
           $cartItem = Cart::find($id);
           if (!$cartItem)return ResponseHelper::errorResponse('Cart item not found', 404);

           $cartItem->delete();

           return ResponseHelper::successResponse('Cart item deleted successfully');
       } catch (\Throwable $th) {
           Log::error([
               'message' => $th->getMessage(),
               'file' => $th->getFile(),
               'line' => $th->getLine()
           ]);

           return ResponseHelper::errorResponse($th->getMessage());
       }
   }
}
