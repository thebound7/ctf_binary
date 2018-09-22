<?php
// create repo object
$repo = new Cz\Git\GitRepository('/path/to/repo');

// create a new file in repo
$filename = $repo->getRepositoryPath() . '/readme.txt';
file_put_contents($filename, "Lorem ipsum
	dolor
	sit amet
");

// commit
$repo->addFile($filename);
$repo->commit('init commit');