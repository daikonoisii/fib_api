import asyncio
from fastapi import APIRouter, Depends,HTTPException
from app.libs.math.fibonacci_number.generate_fibonacci_number import generate_fibonacci_number
from models import FibonacciResultModel,FibonacciValueModel
from concurrent.futures import ProcessPoolExecutor

router = APIRouter()
executor = ProcessPoolExecutor()

@router.get("/fib", response_model=FibonacciResultModel)
async def fibonacci_api_handler(input_value_model: FibonacciValueModel = Depends()) -> dict[str,int]:
    """
    指定された順番のフィボナッチ数を生成するルーター
    ex. n=1 -> 1, n=6 -> 8, n=7 -> 13 n=8 -> 21
    Args:
        input_value_model (FibonacciValueModel) : input_value_model.n
                                                    -> フィボナッチ数列の順番を指定する値.1で先頭のフィボナッチ数を指定する
    Returns:
        FibonacciResultModel(result = fibonacci_number) (FibonacciResultModel) : 指定された番目のフィボナッチ数
    Raises:
        HTTP_422_UNPROCESSABLE_ENTITY: リクエストの内容が不正 or フィボナッチ数を生成する関数が値を処理できなかった
    """

    # イベントループを取得
    loop = asyncio.get_running_loop()

    # n番目のフィボナッチ数を取得
    try:
        # 計算を並列処理で実行
        fibonacci_number:int = await loop.run_in_executor(executor, generate_fibonacci_number, input_value_model.n)
    except ValueError as e:
        # input_value_model.nが1以上の整数ではない
        raise HTTPException(status_code=422, detail=str(e))

    return {"result" : fibonacci_number}