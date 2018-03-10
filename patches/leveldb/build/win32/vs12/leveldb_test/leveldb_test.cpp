// leveldb_test.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include <windows.h>
#include <stdlib.h>
#include <string.h>

#include "include\leveldb\c.h"

int _tmain(int argc, _TCHAR* argv[])
{

	leveldb_t* db;
	leveldb_comparator_t* cmp;
	leveldb_cache_t* cache;
	leveldb_env_t* env;
	leveldb_options_t* options;
	leveldb_readoptions_t* roptions;
	leveldb_writeoptions_t* woptions;
	char* err = NULL;


	env = leveldb_create_default_env();
	cache = leveldb_cache_create_lru(100000);

	options = leveldb_options_create();
	// leveldb_options_set_comparator(options, cmp);
	//leveldb_options_set_error_if_exists(options, 1);
	//leveldb_options_set_cache(options, cache);
	//leveldb_options_set_env(options, env);
	//leveldb_options_set_info_log(options, NULL);
	//leveldb_options_set_write_buffer_size(options, 100000);
	//leveldb_options_set_paranoid_checks(options, 1);
	//leveldb_options_set_max_open_files(options, 10);
	//leveldb_options_set_block_size(options, 1024);
	//leveldb_options_set_block_restart_interval(options, 8);
	leveldb_options_set_compression(options, leveldb_no_compression);

	//roptions = leveldb_readoptions_create();
	//leveldb_readoptions_set_verify_checksums(roptions, 1);
	//leveldb_readoptions_set_fill_cache(roptions, 0);


	woptions = leveldb_writeoptions_create();
	//leveldb_writeoptions_set_sync(woptions, 1); 
	leveldb_writeoptions_set_sync(woptions, 0);

	leveldb_destroy_db(options, "C:/Trace/test.db", &err);

	leveldb_options_set_create_if_missing(options, 1);
	db = leveldb_open(options, "C:/Trace/test.db", &err);



	leveldb_put(db, woptions, "foo", 3, "hello", 5, &err);
	//leveldb_writebatch_t* wb = leveldb_writebatch_create();
	//leveldb_writebatch_put(wb, "foo", 3, "a", 1);
	//leveldb_writebatch_clear(wb);
	//leveldb_writebatch_put(wb, "bar", 3, "b", 1);
	//leveldb_writebatch_put(wb, "box", 3, "c", 1);
	//leveldb_writebatch_delete(wb, "bar", 3);
	//leveldb_write(db, woptions, wb, &err);



	char data[200];
	char key[64];
	LARGE_INTEGER t0, t1, freq;

	QueryPerformanceCounter((LARGE_INTEGER *)&t0);
	unsigned long   last_time = GetTickCount();
	unsigned long    max_time = 0;

	int i, j;
	for (i = 0; i< 5000000; i++) {
		//UpdateTimeString(date,64);
		_itoa(i, key, 10);
		leveldb_put(db, woptions, key, strlen(key), data, 200, &err);

		unsigned long   time = GetTickCount();
		unsigned long   max = time - last_time;
		last_time = time;
		if (max > max_time) {
			max_time = max;
		}
	}

	QueryPerformanceCounter((LARGE_INTEGER *)&t1);

	printf("max_time:%d \n", max_time);

	unsigned long time = (((t1.QuadPart - t0.QuadPart) * 1000000) );

	printf("i:%d time:%f \n", i, time);
	int n = getchar();
	return 0;
}

