let
  pkgs = import <nixpkgs> {};
  libPath = with pkgs; lib.makeLibraryPath [
    libGL
  ];
in
with pkgs; mkShell {
  buildInputs = [
    python3
    python3.pkgs.pip
    libGL
  ];
  shellHook = ''
    # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
    # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH
    pip install -r requirements.txt
  '';
  LD_LIBRARY_PATH = "${libPath}";
}
