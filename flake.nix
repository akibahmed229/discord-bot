{
  description = "Dev Environment for Discord Bot";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
      config = {allowUnfree = true;};
    };
  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "Discord Bot Environment";

      packages = with pkgs; [
        python313Full
        python313Packages.uv
      ];

      # Add shell hooks to the shell environment to be executed on entering the shell
      shellHook = ''
        echo "Entering devShell for ${system}";

        # Persistent virtual environment setup
        if [[ ! -d ./venv ]]; then
          # creating the .venv
          uv sync

          # setting up the .venv permissions
          chmod +x ./.venv/bin/activate
        fi


        source ./.venv/bin/activate

        # workaround for vscode's to find the venv
        venv="$(cd $(dirname $(which python)); cd ..; pwd)"
        ln -Tsf "$venv" .venv
      '';
    };
  };
}
