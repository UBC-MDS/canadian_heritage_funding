# Project: Canadian Heritage Funding
# Authors: Artan Zandian, Joyce Wang, Amelia Tang, Wenxin Xiang
# Usage:  docker run --rm -p 8888:8888 -v /"$(pwd)"://home//jovyan//work image_name

FROM jupyter/minimal-notebook

USER root

# R pre-requisites
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    fonts-dejavu \
    unixodbc \
    unixodbc-dev \
    r-cran-rodbc \
    gfortran \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# R packages including IRKernel which gets installed globally.
# r-e1071: dependency of the caret R package
RUN mamba install --quiet --yes \
    'r-base' \
    'r-caret' \
    'r-crayon' \
    'r-devtools' \
    'r-e1071' \
    'r-hexbin' \
    'r-htmltools' \
    'r-htmlwidgets' \
    'r-irkernel' \
    'r-rcurl' \
    'r-rodbc' \
    'unixodbc' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# These packages are not easy to install under arm
# hadolint ignore=SC2039
RUN set -x && \
    arch=$(uname -m) && \
    if [ "${arch}" == "x86_64" ]; then \
    mamba install --quiet --yes \
    'r-rmarkdown' \
    'r-tidymodels' \
    'r-tidyverse' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"; \
    fi;


# Install Python 3 packages
RUN conda install --quiet -y \
    altair_data_server=0.4.1 \
    altair_saver=0.5.0 \
    altair_viewer=0.3.0 \
    attrs=21.2.0 \
    _py-xgboost-mutex=2.* \
    backcall=0.2.* \
    backports=1.* \
    backports.functools_lru_cache=1.6.* \
    black=21.11b0 \
    blas=2.111 \
    blas-devel=3.9.0 \
    brotlipy=0.7.0 \
    ca-certificates \
    cairo=1.16.0 \
    certifi=2021.10.8 \
    cffi=1.14.6 \
    chardet=4.0.0 \
    charset-normalizer=2.0.0 \
    click=8.0.3 \
    colorama=0.4.4 \
    cryptography=3.4.8 \
    cudatoolkit=11.1.1 \
    cycler=0.10.0 \
    dataclasses=0.8 \
    debugpy=1.4.1 \
    decorator=5.1.0 \
    docopt=0.6.2 \
    entrypoints=0.3 \
    expat=2.4.1 \
    font-ttf-dejavu-sans-mono=2.37 \
    font-ttf-inconsolata=3.000 \
    font-ttf-source-code-pro=2.038 \
    font-ttf-ubuntu=0.83 \
    fontconfig=2.13.1 \
    fonts-conda-ecosystem=1 \
    fonts-conda-forge=1 \
    freetype=2.10.4 \
    fribidi=1.0.10 \
    gettext=0.19.8.1 \
    graphite2=1.3.13 \
    graphviz=2.49.1 \
    gts=0.7.6 \
    harfbuzz=3.0.0 \
    icu=68.1 \
    idna=3.1 \
    importlib-metadata=4.8.1 \
    ipykernel=6.4.1 \
    ipython=7.28.0 \
    ipython_genutils=0.2.0 \
    jbig=2.1 \
    jedi=0.18.0 \
    jinja2=3.0.2 \
    joblib=1.1.0 \
    jpeg=9d \
    jsonschema=4.1.0 \
    jupyter_client=7.0.6 \
    jupyter_core=4.8.1 \
    kiwisolver=1.3.2 \
    lcms2=2.12 \
    lerc=2.2.1 \
    libblas=3.9.0 \
    libcblas=3.9.0 \
    libclang=11.1.0 \
    libdeflate=1.7 \
    libffi=3.4.2 \
    libgd=2.3.3 \
    libglib=2.68.4 \
    libiconv=1.16 \
    liblapack=3.9.0 \
    liblapacke=3.9.0 \
    libpng=1.6.37 \
    libsodium=1.0.18 \
    libtiff=4.3.0 \
    libuv=1.42.0 \
    libwebp=1.2.1 \
    libwebp-base=1.2.1 \
    libxcb=1.13 \
    libxgboost=1.4.2 \
    libxml2=2.9.12 \
    libzlib=1.2.11 \
    lightgbm=3.2.1 \
    lz4-c=1.9.3 \
    markupsafe=2.0.1 \
    mkl=2021.3.0 \
    mkl-devel=2021.3.0 \
    mkl-include=2021.3.0 \
    mypy_extensions=0.4.3 \
    nest-asyncio=1.5.1 \
    ninja=1.10.2 \
    nodejs=14.17.4 \
    numpy=1.21.2 \
    olefile=0.46 \
    openjpeg=2.4.0 \
    openssl=1.1.1l \
    pandas=1.3.3 \
    pandoc=2.16.2 \
    pango=1.48.10 \
    parso=0.8.2 \
    pathspec=0.9.0 \
    pcre=8.45 \
    pickleshare=0.7.5 \
    pillow=8.3.2 \
    pip=21.2.4 \
    pixman=0.40.0 \
    platformdirs=2.3.0 \
    portpicker=1.4.0 \
    prompt-toolkit=3.0.20 \
    pthread-stubs=0.4 \
    py-xgboost=1.4.2 \
    pycparser=2.20 \
    pygments=2.10.0 \
    pyopenssl=21.0.0 \
    pyparsing=2.4.7 \
    pyqt=5.12.3 \
    pyqt-impl=5.12.3 \
    pyqt5-sip=4.19.18 \
    pyqtchart=5.12 \
    pyqtwebengine=5.12.1 \
    pyrsistent=0.17.3 \
    pysocks=1.7.1 \
    python=3.9.7 \
    python-dateutil=2.8.2 \
    python-graphviz=0.17 \
    python_abi \
    pytz=2021.3 \
    pyzmq=22.3.0 \
    qt=5.12.9 \
    regex=2021.11.10 \
    requests=2.26.0 \
    scikit-learn=1.0 \
    scipy=1.7.1 \
    selenium=3.141.0 \
    setuptools=58.2.0 \
    six=1.16.0 \
    tbb=2021.3.0 \
    threadpoolctl=3.0.0 \
    tk=8.6.11 \
    tomli=1.2.2 \
    toolz=0.11.1 \
    tornado=6.1 \
    traitlets=5.1.0 \
    typed-ast=1.5.0 \
    typing_extensions=3.10.0.2 \
    tzdata=2021c \
    urllib3=1.26.7 \
    wcwidth=0.2.5 \
    wheel=0.37.0 \
    xgboost=1.4.2



# Install dependancy for altair to save png files
RUN npm install -g npm vega vega-cli vega-lite canvas -f


# Install R packages

