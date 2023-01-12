SKIP_UPDATE=$1

PORT=$(python -c "import random; print(random.randint(2000, 3000))")

python killall.py
rm *.log

if [ -z "$SKIP_UPDATE" ]
then
    for team in `ls teams`
    do
        echo "#################"
        echo "Updating $team"
        cd teams/$team
        git pull
        cd -
    done
fi

python -m chronobio.game.server -p $PORT &
python -m chronobio.viewer -p $PORT &
sleep 2

for team in `ls teams`
do
    echo "#################"
    echo "Starting $team"
    cd teams/$team
    ./_launch.sh $PORT &
    cd -
done

sleep 600
python killall.py
