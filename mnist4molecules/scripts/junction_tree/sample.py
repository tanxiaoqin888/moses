import sys
sys.path.insert(0, '..')

import argparse
import pandas as pd
import rdkit
import torch
import tqdm

from mnist4molecules.junction_tree.config import get_parser
from mnist4molecules.junction_tree.jtnn.jtnn_vae import JTNNVAE
from utils import add_sample_args, set_seed


lg = rdkit.RDLogger.logger()
lg.setLevel(rdkit.RDLogger.CRITICAL)


def main(config):
    set_seed(config.seed)

    model_vocab = torch.load(config.vocab_load)
    model_config = torch.load(config.config_load)
    model_state = torch.load(new_config.model_load)

    device = torch.device(config.device)

    model = JTNNVAE(model_vocab, model_config.hidden, model_config.latent, model_config.depth)
    model.load_state_dict(model_state)
    model = model.to(device=device)

    gen_smiles = []
    for i in tqdm.tqdm(range(config.n_samples)):
        gen_smiles.append(model.sample_prior())

    df = pd.DataFrame(gen_smiles, columns=['SMILES'])
    df.to_csv(config.gen_save, index=False)


if __name__ == '__main__':
    parser = add_sample_args(argparse.ArgumentParser())
    config = parser.parse_known_args()[0]
    main(config)