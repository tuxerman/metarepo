# #!/bin/bash

# # python dataFiller.py 1000,10000,50000,1

# echo '------------------------------------------------------' >> ./logs/dataserver.log
# python -m cProfile -s time serverEngine.py 10 >> ./logs/dataserver.log

# echo '------------------------------------------------------' >> ./logs/dataserver.log
# python -m cProfile -s time serverEngine.py 20 >> ./logs/dataserver.log

# echo '------------------------------------------------------' >> ./logs/dataserver.log
# python -m cProfile -s time serverEngine.py 40 >> ./logs/dataserver.log

# echo '------------------------------------------------------' >> ./logs/dataserver.log
# python -m cProfile -s time serverEngine.py 80 >> ./logs/dataserver.log

# echo '------------------------------------------------------' >> ./logs/dataserver.log
# python -m cProfile -s time serverEngine.py 160 >> ./logs/dataserver.log

# echo '------------------------------------------------------' >> ./logs/dataserver.log
# python -m cProfile -s time serverEngine.py 320 >> ./logs/dataserver.log

echo '------------------------------------------------------' >> ./logs/dataserver2.log
python -m cProfile -s time dataFiller.py 100,1000,5000,1 >> ./logs/dataserver2.log
python -m cProfile -s time serverEngine.py 20 >> ./logs/dataserver2.log

echo '------------------------------------------------------' >> ./logs/dataserver2.log
python -m cProfile -s time dataFiller.py 100,2000,5000,1 >> ./logs/dataserver2.log
python -m cProfile -s time serverEngine.py 20 >> ./logs/dataserver2.log

echo '------------------------------------------------------' >> ./logs/dataserver2.log
python -m cProfile -s time dataFiller.py 100,4000,5000,1 >> ./logs/dataserver2.log
python -m cProfile -s time serverEngine.py 20 >> ./logs/dataserver2.log

echo '------------------------------------------------------' >> ./logs/dataserver2.log
python -m cProfile -s time dataFiller.py 100,8000,5000,1 >> ./logs/dataserver2.log
python -m cProfile -s time serverEngine.py 20 >> ./logs/dataserver2.log