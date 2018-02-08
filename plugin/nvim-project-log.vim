nnoremap <space>l :ProjectLogToday<CR>
nnoremap <space>i :ProjectLogIndex<CR>
nnoremap <space>gi :ProjectLogUpdateIndex<CR>

augroup project_log#Navigation
    autocmd!
    autocmd BufRead,BufNewFile */????-??-??.md nnoremap <buffer> <down> :ProjectLogPrevious<CR>
    autocmd BufRead,BufNewFile */????-??-??.md nnoremap <buffer> <up> :ProjectLogNext<CR>
augroup END

if !exists("g:project_log#logbooks")
    let g:project_log#logbooks = [$HOME.'/notes']
endif

if !exists("g:project_log#log_level")
    let g:project_log#log_level = 'INFO'
endif
