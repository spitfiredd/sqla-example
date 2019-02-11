# sqlalchemy-examples

Testing ground for various ideas or use cases for sqlalchemy.

## Getting Started

You will need to have python and pipenv installed on your machine. To get your envrionment setup with the package dependencies run `pipenv install --ignore-pipfile` this will used the `Pipfile.lock` to create the same environment as the last time you ran `pipenv lock`.

After you environment is setup run `pipenv shell` to activate your environment.

You can now run an example, for example,

```
python -m examples.products.app
```

### TsVector Example

This examples will create a searchable column using postgres built in `tsvector_update_trigger`, to run the examples execute the following,

```
python -m examples.tsvector.create
python -m examples.tsvector.populate
```

Running those two scripts will populate a sample database using [Faker][1] to generate fake data.  If you want to drop the table run `python -m examples.tsvector.drop` with drop using `CASCADE`.

Here is an example of my table,

![Image of Table][2]


More examples coming soon!!

## Running the tests

Explain how to run the automated tests for this system


## Deployment

Add additional notes about how to deploy this on a live system

## Contributing

Use git flow principals, fork develop branch to your repo and create a new feature or bug fix branch. Once done submit a pull request to merge your changes to the develop branch.

## Versioning

Will probably use versioneer at some later date.

## Authors

* **Daniel Donovan** - *Initial work* - [email](mailto:spitfiredd@gmail.com)

## License


[1]: https://faker.readthedocs.io/en/latest/providers/faker.providers.python.html
[2]: https://i.imgur.com/KYbQN9H.png