{
  description = "Python application flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      runtimeDeps = with pkgs.python3Packages; [deepl];
      buildDeps = with pkgs.python3Packages; [setuptools];
    in {
      packages = rec {
        deepl = pkgs.python3Packages.buildPythonApplication {
          pname = "deepl";
          version = "0.1";
          pyproject = true;
          propagatedBuildInputs = runtimeDeps ++ buildDeps;
          src = ./.;
        };
        default = deepl;
      };

      devShells.default = pkgs.mkShell {buildInputs = runtimeDeps;};
    })
    // {
      overlays.default = final: prev: {shoppy = self.packages.${prev.system}.default;};
    };
}
