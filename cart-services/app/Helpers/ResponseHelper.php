<?php
namespace App\Helpers;

class ResponseHelper
{
    public static function successResponse($message, $data = null)
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data
        ], 200);
    }

    public static function errorResponse($message, $status = 500)
    {
        return response()->json([
            'success' => false,
            'message' => $message
        ], $status);
    }
}
