{
  description = "IQM Quantum School project dev env";

  # inputs = {
  #   nixpkgs.url = "github:NixOS/nixpkgs";
  # };

  outputs = { self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        uv
        zed-editor
      ];

      shellHook = ''
        echo "IQM Nix dev shell active"
      '';
    };
  };
}
