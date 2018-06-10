# Spatial Temporal Adaptive Reflectance Fusion Model (STARFM)

This is a short implementation of STARFM algorithm in Python language

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Here are some dependencies to make this project work.
Numpy for the matrix computation. While, tqdm only to beautify this project processing time :) .

```
Numpy
tqdm
```

### Installing

Do this to install them


```
pip install numpy tqdm
```

## Running the tests

To start your first prediction, change these three line
in compute.py according to your input filenames

```
Lkpixel = "WV_blue_1812.txt"
Mkpixel = "L8_blue_0701.txt"
M0pixel = "L8_blue_0411.txt"

```

then, change the pixel dimension variable according to your input pixel here in compute.py and write.py

```
pixel_dimension = 1125
```

Then, run this to predict

```
python compute.py
```

## Built With

* [Numpy](http://www.dropwizard.io/1.0.2/docs/) - Scientific computation support
* [tqdm](https://github.com/tqdm/tqdm) - Used to generate progress bar

## Authors

* **Hari Setiawan** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
