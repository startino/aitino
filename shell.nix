{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
    name = "pipzone";
    targetPkgs = pkgs: (with pkgs; [
        python311
        python311Packages.pip
    ]);
    runScript = "fish";
}).env
