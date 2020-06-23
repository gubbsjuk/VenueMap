import os
import random
import string

def write_dot_env_file(env_file):
    settings = get_settings()
    with open(env_file, 'w') as f:
        for k, v in settings.items():
            f.write(f'{k.upper()}={v}\n')

def get_settings():
    return{
        'SECRET_KEY': generate_secret_key(),
        'DEBUG': False,
        'ALLOWED_HOSTS': '', #* ?
    }

def generate_secret_key():
    specials = '!@#$%^&*(-_=+)'
    chars = string.ascii_lowercase + string.digits + specials
    return ''.join(random.choice(chars) for _ in range(50))

def main():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

    if not os.path.isfile(env_file):
        write_dot_env_file(env_file)
    else:
        pass


if __name__ == '__main__':
    main()