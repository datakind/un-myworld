# Normalizes country names from http://hdrstats.undp.org/en/tables/ to use with MYWorld names
# Pass file name as first arg i.e. './normalize.sh $1'
sed -i '' 's/Congo (Democratic Republic of the)/democratic republic of the congo/g' $1
sed -i '' "s/Côte d\'Ivoire/cote d'ivoire/g" $1
sed -i '' "s/Palestine, State of/palestine (state of)/g" $1
sed -i '' "s/Korea (Democratic People\'s Rep. of)/democratic people's republic of korea/g" $1
sed -i '' "s/Korea (Republic of)/republic of korea/g" $1
sed -i '' "s/Tanzania (United Republic of)/united republic of tanzania/g" $1
sed -i '' "s/United Kingdom/united kingdom of great britain and northern ireland/g" $1
sed -i '' "s/United States/united states of america/g" $1
sed -i '' "s/Moldova (Republic of)/republic of moldova/g" $1
sed -i '' "s/Hong Kong, China (SAR)/china/g" $1
