{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    parts = {
      url = "github:gibbz00/parts";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-parts.follows = "flake-parts";
    };
  };

  outputs =
    inputs@{ nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.systems.flakeExposed;

      imports = [
        inputs.parts.flakeModule.pre-commit
        inputs.parts.flakeModule.python
      ];

      perSystem =
        {
          config,
          pkgs,
          lib,
          ...
        }:
        {
          pre-commit.settings.hooks.typos.enable = lib.mkForce false;

          devShells.default = pkgs.mkShell {
            name = "mve780-laborationer";

            inputsFrom = [
              config.devShells.pre-commit
              config.devShells.python
            ];

            packages = with pkgs; [
              python314Packages.numpy
              python314Packages.matplotlib
              python314Packages.tabulate
            ];
          };
        };
    };
}
