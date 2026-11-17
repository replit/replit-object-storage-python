{
  description = "Reproducible checks for the Object Storage Python client";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { nixpkgs, poetry2nix, ... }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      inherit (pkgs) lib;
      dependencies = lib.fileset.toSource {
        root = ./.;
        fileset = lib.fileset.unions [ ./pyproject.toml ./poetry.lock ];
      };
      poetry = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
      python = poetry.mkPoetryEnv {
        projectDir = dependencies;
        python = pkgs.python310;
        preferWheels = true;
        groups = [ "main" ];
        checkGroups = [ ];
        extraPackages = ps: [ ps.ruff ps.pytest ps.pytest-cov ];
        overrides = poetry.defaultPoetryOverrides.extend (_final: prev: {
          fetchFromPypi = args: (prev.fetchFromPypi args).overrideAttrs (old:
            let
              parts = lib.splitString "-" args.file;
              pythonTag = builtins.elemAt parts (builtins.length parts - 3);
            in
            {
              # PyPI's wheel redirect uses the Python tag, not a literal "wheel".
              predictedURL = builtins.replaceStrings
                [ "/wheel/" ] [ "/${pythonTag}/" ] old.predictedURL;
            });
        });
      };
      source = lib.fileset.toSource {
        root = ./.;
        fileset = lib.fileset.unions [ ./src ./tests ./pyproject.toml ];
      };
    in
    {
      checks.x86_64-linux = {
        lint = pkgs.runCommand "object-storage-lint" { nativeBuildInputs = [ python ]; } ''
          cp -r ${source} source
          chmod -R u+w source
          cd source
          ruff check src tests
          touch "$out"
        '';
        unit = pkgs.runCommand "object-storage-unit" { nativeBuildInputs = [ python ]; } ''
          cp -r ${source} source
          chmod -R u+w source
          cd source
          export PYTHONPATH="$PWD/src"
          pytest --cov-report term-missing --cov=./src ./tests/unit
          mkdir -p "$out"
          cp .coverage "$out/"
        '';
      };
    };
}
