# CRISPR

# How was I generated?
1. Download code from https://github.com/chunkunbo/CRISPR
2. Run both example usages in CRISPR/ANML
3. python anml_gen_casoffinder.py 100.txt 1
4. python anml_gen_casot.py 100.txt 2 3
5. rename each STE in each file with a prefix OT or OFF

# CRISPR_CasOFFinder_2000.anml

## How was I generated?

``` python
python input_generator.py 2000 agg 7 > 2000.txt
python anml_gen_casoffinder.py 2000.txt 1 > CRISPR_CasOFFinder_2000.anml
```

# CRISPR_CasOT_2000.anml

## How was I generated?
``` python
python input_generator.py 2000 agg 7 > 2000.txt
python anml_gen_casot.py 2000.txt 2 3 > CRISPR_CasOT_2000.anml
```

 