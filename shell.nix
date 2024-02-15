{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
    name = "pipzone";
    targetPkgs = pkgs: (with pkgs; [
        python311
        python311Packages.pip
        pipx
        poetry
    ]);
    runScript = "fish";
}).env
