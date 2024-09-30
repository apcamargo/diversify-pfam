# `diversify-pfam`

`diversify-pfam` is a tool designed to generate alternative alignments and HMMER Hidden Markov Models (HMMs) for a specified Pfam accession or an input Multiple Sequence Alignment (MSA) file. Its primary aim is to improve the detection sensitivity of orthologous sequences by leveraging HMMs derived from various alignments.

Here's an overview of the steps involved:

1. **Download alignments**: Retrieve the seed and full alignments for a given Pfam accession from [InterPro](https://www.ebi.ac.uk/interpro/) through its [API](https://github.com/ProteinsWebTeam/interpro7-api/blob/master/docs/README.md). If the `--msa-file` option is used, the script will read an input MSA file instead of downloading alignments.
2. **Preprocess full alignment:** Remove unaligned columns (containing lowercase characters) from the full alignment.
3. **Reduce redundancy:** Generate alignments with reduced redundancy by clustering the full alignment at 90% and 50% sequence identity.
4. **Enrich alignment:** Use HHblits to search one or more clustered databases (e.g., [UniRef30](https://gwdu111.gwdg.de/~compbiol/uniclust/2023_02/) and [BFD](https://bfd.mmseqs.com/)) to generate an enriched alignment from the seed alignment. To disable this step, use the `--disable-enrichment` option.
5. **Cluster alignments:** Cluster the full alignment, the non-redundant alignments (at 90% and 50% identity), and the enriched alignment using [`cluster_msa.py`](https://github.com/apcamargo/cluster_msa) to generate subalignments. To disable this step, use the `--disable-clustering` option.
6. **Generate HMMs:** Create HMMER HMMs from all alignments: seed, full, non-redundant at 50% identity, non-redundant at 90% identity, enriched, and subalignments. Note that the seed alignment is not clustered and therefore does not produce subalignments.

## Dependencies

All dependencies are automatically installed by [Pixi](https://pixi.sh/) when the tool is executed for the first time, so you don't need to install them manually. The following tools and libraries are used:

### External tools

- [HH-suite](https://github.com/soedinglab/hh-suite) (`hhblits`, `hhfilter`, and `reformat.pl` commands)
- [HMMER](http://hmmer.org/) (`esl-alimask` command)
- [seqkit](https://bioinf.shenwei.me/seqkit/)

### Python libraries

- [Biopython](https://biopython.org/)
- [NumPy](https://numpy.org/)
- [Polyleven](https://ceptord.net/)
- [PyHMMER](https://pyhmmer.readthedocs.io/en/stable/)
- [scikit-learn](https://scikit-learn.org/stable/)
- [sh](https://sh.readthedocs.io/en/latest/)

## Usage

```sh
$ git clone --recursive https://github.com/apcamargo/diversify_pfam.git
$ cd diversify-pfam
$ pixi run diversify-pfam -h
```

    Usage: diversify-pfam [OPTIONS] PFAM OUTPUT_DIR OUTPUT_HMM_FILE

    Options:
    -m, --msa-file              Input is a multiple sequence alignment FASTA
                                file
    -d, --database TEXT         HHblits database(s)
    --disable-enrichment        Disable MSA enrichment with HHblits
    --disable-clustering FLOAT  Disable MSA clustering into subalignments
    --ascii-hmm                 Output ASCII HMM instead of the binary format.
    --gathering-cutoff FLOAT    Set the gathering cutoff value for the resulting
                                HMMs
    --verbose                   Enable verbose mode
    -h, --help                  Show this message and exit.

### Positional arguments

| Argument     | Description                                                                                      |
| :----------- | :----------------------------------------------------------------------------------------------- |
| `pfam`       | The accession of the Pfam that will be downloaded and processed, or the path to a MSA FASTA file |
| `output_dir` | The directory where output MSA files will be stored                                              |
| `output_hmm` | The output HMM file                                                                              |

### Options

| Option                                    | Description                                         | Default |
| :---------------------------------------- | :-------------------------------------------------- | :------ |
| `-m MSA_FILE`, `--msa-file`               | Input is a multiple sequence alignment FASTA file   | False   |
| `-d DATABASE`, `--database DATABASE`      | HHblits database(s)                                 | None    |
| `--disable-enrichment`                    | Disable MSA enrichment with HHblits                 | False   |
| `--disable-clustering DISABLE_CLUSTERING` | Disable MSA clustering into subalignments           | None    |
| `--ascii-hmm`                             | Output ASCII HMM instead of binary format           | False   |
| `--gathering-cutoff GATHERING_CUTOFF`     | Set gathering cutoff value for resulting HMMs       | None    |
| `--verbose`                               | Enable verbose mode                                 | False   |

## Example

```sh
$ pixi run diversify-pfam PF02387 MSAs PF02387_div.h3m -d $DATABASES/UniRef30_2023_02/UniRef30_2023_02 -d $DATABASES/BFD/BFD --verbose
```

    [2024-08-18 21:47:14] Creating output directory 'MSAs'…
    [2024-08-18 21:47:14] Downloading 'PF02387' seed and full alignments…
    [2024-08-18 21:47:16] Converting seed and full alignments to the FASTA format and removing unaligned columns…
    [2024-08-18 21:47:16] Removing redundancy of the full MSA at 90% and 50% sequence identity…
    [2024-08-18 21:47:16] Performing HHblits enrichment…
    [2024-08-18 21:49:41] Generating clustered alignments for the full MSA…
    [2024-08-18 21:49:42] Generating clustered alignments for the 50% non-redundant MSA…
    [2024-08-18 21:49:42] Generating clustered alignments for the 90% non-redundant MSA…
    [2024-08-18 21:49:43] Generating clustered alignments for HHblits-enriched MSA…
    [2024-08-18 21:49:48] Generating HMMs and writing to 'PF02387_div.h3m'…

```sh
$ tree MSAs
```

    MSAs
    ├── PF02387_50.afa
    ├── PF02387_50_cluster_0.afa
    ├── PF02387_90.afa
    ├── PF02387_90_cluster_0.afa
    ├── PF02387_90_cluster_1.afa
    ├── PF02387_90_cluster_2.afa
    ├── PF02387_enriched.afa
    ├── PF02387_enriched_cluster_0.afa
    …
    └── PF02387_seed.afa

```sh
$ hmmconvert -a PF02387_div.h3m
```

    HMMER3/f [3.4 | Aug 2023]
    NAME  PF02387_50
    ACC   PF02387_50
    LENG  260
    ALPH  amino
    …
