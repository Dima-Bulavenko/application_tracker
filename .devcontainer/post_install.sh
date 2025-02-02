#/bin/sh

set -e

# Install required packages
apk add zsh nano zsh-vcs git less git-doc man-pages mandoc


# Install Oh-My-ZSH
sh -c "$(wget -qO- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended


# Install plugins
# https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md#oh-my-zsh
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Add plugins in .zshrc if not already present
if ! grep -q "zsh-syntax-highlighting" ~/.zshrc; then
    sed -i '/^plugins=/ s/)/ zsh-syntax-highlighting)/' ~/.zshrc
fi

# Must be at the end of the "plugins" list
if ! grep -q "zsh-autosuggestions" ~/.zshrc; then
    sed -i '/^plugins=/ s/)/ zsh-autosuggestions)/' ~/.zshrc
fi


# Install theme
# https://github.com/spaceship-prompt/spaceship-
git clone https://github.com/spaceship-prompt/spaceship-prompt.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/spaceship-prompt --depth=1
ln -s ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/spaceship-prompt/spaceship.zsh-theme ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/spaceship.zsh-theme

# Set ZSH_THEME to "spaceship"
if grep -q "^ZSH_THEME=" ~/.zshrc; then
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="spaceship"/' ~/.zshrc
else
    echo 'ZSH_THEME="spaceship"' >> ~/.zshrc
fi

touch ~/.spaceshiprc.zsh
cat ../.devcontainer/.spaceshiprc.zsh >> ~/.spaceshiprc.zsh
