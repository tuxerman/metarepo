#!/bin/bash

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,10 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,20 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,40 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,60 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,120 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,240 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,480 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 2000,10000,50000,50 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 4000,10000,50000,50 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 8000,10000,50000,50 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,10000,50000,50 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,20000,50000,50 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,40000,50000,50 >> ./logs/datafiller.log

# echo '------------------------------------------------------' >> ./logs/datafiller.log
# python -m cProfile -s time dataFiller.py 1000,80000,50000,50 >> ./logs/datafiller.log

echo 'NEXT ONE...'
echo '------------------------------------------------------' >> ./logs/datafillerTrans.log
python -m cProfile -s time dataFiller.py 1000,1000,1500,2 >> ./logs/datafillerTrans.log

echo 'NEXT ONE...'
echo '------------------------------------------------------' >> ./logs/datafillerTrans.log
python -m cProfile -s time dataFiller.py 1000,2000,1500,2 >> ./logs/datafillerTrans.log

echo 'NEXT ONE...'
echo '------------------------------------------------------' >> ./logs/datafillerTrans.log
python -m cProfile -s time dataFiller.py 1000,5000,1500,2 >> ./logs/datafillerTrans.log

echo 'NEXT ONE...'
echo '------------------------------------------------------' >> ./logs/datafillerTrans.log
python -m cProfile -s time dataFiller.py 1000,10000,1500,2 >> ./logs/datafillerTrans.log

echo 'NEXT ONE...'
echo '------------------------------------------------------' >> ./logs/datafillerTrans.log
python -m cProfile -s time dataFiller.py 1000,15000,1500,2 >> ./logs/datafillerTrans.log

echo 'NEXT ONE...'
echo '------------------------------------------------------' >> ./logs/datafillerTrans.log
python -m cProfile -s time dataFiller.py 1000,20000,1500,2 >> ./logs/datafillerTrans.log