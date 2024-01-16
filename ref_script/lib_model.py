import torch
import torch.nn as nn


class VAE(nn.Module):
    def __init__(self, latent_dim):
        super().__init__()

        self.latent_dim = latent_dim
        self.encoder = self.buildEncoder(latent_dim)
        self.decoder = self.buildDecoder(latent_dim)

    def buildEncoder(self, latent_dim):
        encoder = nn.Sequential(

            nn.Conv2d(in_channels=2, out_channels=8, kernel_size=3, stride=2, padding=1),
            nn.ELU(),

            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=2, padding=1),
            nn.ELU(),

            nn.ConstantPad3d((0, 1, 0, 0), 0),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=2, padding=1),
            nn.ELU(),

            nn.ConstantPad3d((0, 0, 0, 1), 0),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2, padding=1),
            nn.ELU(),

            nn.ConstantPad3d((0, 1, 0, 0), 0),
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1),
            nn.ELU(),

            nn.ConstantPad3d((0, 0, 0, 1), 0),
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1),
            nn.ELU(),

            nn.Flatten(start_dim=1, end_dim=-1),

            nn.Linear(2560, 256),
            nn.ELU(),

            nn.Linear(256, latent_dim * 2),
        )
        return encoder


    def buildDecoder(self, latent_dim):
        decoder = nn.Sequential(

            nn.Linear(latent_dim, 256),
            nn.ELU(),

            nn.Linear(256, 256 * 5 * 2),
            nn.ELU(),

            nn.Unflatten(dim=1, unflattened_size=(256, 2, 5)),

            nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ConstantPad2d((0, 0, 0, -1), 0),
            nn.ELU(),

            nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ConstantPad2d((0, -1, 0, 0), 0),
            nn.ELU(),

            nn.ConvTranspose2d(in_channels=64, out_channels=32, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ConstantPad2d((0, 0, 0, -1), 0),
            nn.ELU(),

            nn.ConvTranspose2d(in_channels=32, out_channels=16, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ConstantPad2d((0, -1, 0, 0), 0),
            nn.ELU(),

            nn.ConvTranspose2d(in_channels=16, out_channels=8, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ConstantPad2d((0, 0, 0, 0), 0),
            nn.ELU(),

            nn.ConvTranspose2d(in_channels=8, out_channels=2, kernel_size=3, stride=2, padding=1, output_padding=1),

        )
        return decoder

    def sample(self, mean, logvariance):

        std = torch.exp(0.5 * logvariance)
        epsilon = torch.rand_like(std)

        return mean + epsilon*std

    def forward(self, data):

        mean_logvariance = self.encoder(data)

        mean, logvariance = torch.chunk(mean_logvariance, 2, dim=1)

        z = self.sample(mean, logvariance)

        reconstruction = self.decoder(z)

        return reconstruction, mean, logvariance

    # def forward(self, data):
    #
    #     mean_logvariance = self.encoder(data)
    #
    #     return mean_logvariance


def save_checkpoint(state, path_name):

    print('Saving checkpoint')

    torch.save(state, path_name)

    print('Saved checkpoint')


def load_checkpoint(model, path_name, optimizer=None):

    print('Loading checkpoint')
    print(path_name)

    checkpoint = torch.load(path_name)
    model.load_state_dict(checkpoint['state_dict'])
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint['optimizer_dict'])

    print('Loaded checkpoint')

'''Testing code'''
if __name__ == "__main__":
    from torchsummary import summary

    example = VAE(latent_dim=10).to('cuda')
    summary(example, input_size=(2, 88, 300))