# Detecting bots in wikipedia streaming data
### *Mining Massive Databases Final Project*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GCmsU5s-HTEUvZmogIYj5YtKTMVnHVn8?usp=sharing)

## The team
- Olena Ivina, ivina.pn@ucu.edu.ua
- Oleksandr Khrystoforov, o.khrystoforov@ucu.edu.ua
- Andrii Kapatsyn, kapatyn.pn@ucu.edu.ua


## Project description

The project is about detecting bots in wikipedia streaming data for all the edits done (`requestchanges` thread). The key `"bot"` in the responce is used as a target in training and analysis process. As result we should develop a system that detects bots in realtime streaming data. The main technology used is spark.

The exact task is the following:
- Consider all the changes done in the wikipedia as stream.
    Check here: https://wikitech.wikimedia.org/wiki/RCStream
- Each action is received in `json` format.
- Data is full of bots. There is a flag were programmers can
indicate that an actions has been done by a bot.
- Using this information as ground truth, develop a system able
to classify users as bot or human.
- **Constrain: You need to sample, and just use the `20%` of
the data stream.**
- Describe the distribution of edits per users and bots.
- Finally, train a Bloom Filter that filter out bots from the stream.
    - Find the correct parameters for the bloom filter having an error below `10%`.
- If you want to have a `100%` you need to do this:
    - Make your system to work with Spark Streaming (`5%`)


## Project structure

The project is divided by folders, related to the each step:
- `fetch_data` - Scripts to serialize wikipedia changes stream into `.jsonl` files
- `classify_data` - Analysis, data preparation, and classifier training scripts
- `bloom_filter` - Implementation and usage of bloom filter
- `inference` - Application that detects bots in real time using pre-trained bloom filter


## How to run demo

The demo includes initialization of pre-trained bloom filter and running it on either validation sampled stream or real time stream data.

The demo is available in the colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GCmsU5s-HTEUvZmogIYj5YtKTMVnHVn8?usp=sharing)
