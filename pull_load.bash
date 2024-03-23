#!/bin/bash 

today=$(date +%Y-%m-%d+%T)  
# echo "$today --- $0 $1  " >> /opt/CurrencyRatingAnalysis/logs/log.txt 2>&1
echo "$0: $today : started on $1 " >> /opt/CurrencyRatingAnalysis/logs/log.txt 2>&1

#echo "nuber of agrs = $#"
#echo $1

if [ "$#" -eq 0 ]; then
  echo "Please specify environment, dev or prod."
  exit 1
elif [ "$#" -gt 0 ] && [ $1 != "dev" ] && [ $1 != "prod" ]; then  
        echo "Wrong environment: $1. Only dev and prod are permitted."
        exit 1
elif [ "$#" -gt 1 ]; then
  echo "Extra arguments are ignored."    
fi

/home/leonid/anaconda3/envs/py-3.11-CurRates/bin/python /opt/CurrencyRatingAnalysis/bin/prior_get_content.py $1 >> /opt/CurrencyRatingAnalysis/logs/log.txt 2>&1
/home/leonid/anaconda3/envs/py-3.11-CurRates/bin/python /opt/CurrencyRatingAnalysis/bin/Raw2Rates.py $1 >> /opt/CurrencyRatingAnalysis/logs/log.txt 2>&1

exit 0

