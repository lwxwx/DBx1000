#ifndef _SEQUENCER_H_
#define _SEQUENCER_H_

#include "global.h"
#include "query.h"
//#include "helper.h"

class workload;

typedef struct qlite_entry {
	uint32_t client_id;
	uint64_t client_startts;
	uint32_t server_ack_cnt;
} qlite;

class Sequencer {
 public:
	void init(workload * wl);	
	void process_txn_ack(base_client_query * query, uint64_t thd_id);
	void process_new_txn(base_client_query * query);
	//void start_batch_timer();
	void send_first_batch(uint64_t thd_id); 
	WorkQueue * fill_queue;		// queue currently being filled with new txns
	WorkQueue * batch_queue;	// queue being batched & processed
	volatile uint64_t total_txns_finished;
	volatile uint64_t total_txns_received;
	volatile bool sent_first_batch;
	volatile uint32_t rsp_cnt;
 private:
	void prepare_next_batch(uint64_t thd_id);
	void reset_participating_nodes(bool * part_nodes);
	qlite * wait_list;		// list of txns in batch being executed
	uint64_t wait_list_size;
	uint32_t wait_txns_left;
	volatile uint32_t next_txn_id;
	volatile uint64_t next_batch_id;
	pthread_mutex_t mtx;
	pthread_cond_t swap_cv;	// thread is swapping fill and batch queues
	pthread_cond_t access_cv;	// thread(s) are accessing fill and/or batch queues
	volatile bool swapping_queues;
	volatile uint32_t num_accessing_queues;
	pthread_mutex_t batchts_mtx;
	volatile uint64_t batch_ts;	// time since last batch was sent
	workload * _wl;
};

class Seq_thread_t {
public:
	uint64_t _thd_id;
	uint64_t _node_id;
	workload * _wl;

	uint64_t 	get_thd_id();
	uint64_t 	get_node_id();


	void 		init(uint64_t thd_id, uint64_t node_id, workload * workload);
	// the following function must be in the form void* (*)(void*)
	// to run with pthread.
	// conversion is done within the function.
	//RC 			run();
	RC 			run_remote();
};
#endif