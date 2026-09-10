{
  description = "PowerQuest-AI dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python3
            pkgs.python3Packages.pip
            pkgs.python3Packages.venvShellHook
          ];

          # pyboy/numpy ship pip binary wheels that expect these libs to be
          # on the system loader path -- not the case on NixOS by default.
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
          ];

          venvDir = "./.venv";

          postVenvCreation = ''
            pip install --quiet -r requirements.txt
          '';

          postShellHook = ''
            echo "PowerQuest-AI dev shell ready. Venv: $venvDir"
          '';
        };
      });
}
